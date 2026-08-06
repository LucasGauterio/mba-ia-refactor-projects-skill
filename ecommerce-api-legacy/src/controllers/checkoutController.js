const CourseModel = require('../models/courseModel');
const UserModel = require('../models/userModel');
const CheckoutModel = require('../models/checkoutModel');
const { logAndCache } = require('../utils/cache');
const { hashPassword } = require('../config/security');
const settings = require('../config/settings');

class CheckoutController {
    static async checkout(req, res, next) {
        try {
            const { usr, eml, pwd, c_id, card } = req.body;

            // Basic validation
            if (!usr || !eml || !c_id || !card) {
                return res.status(400).send("Bad Request");
            }

            // Find course
            const course = await CourseModel.findActiveById(c_id);
            if (!course) {
                return res.status(404).send("Curso não encontrado");
            }

            // Find or create user
            let user = await UserModel.findByEmail(eml);
            let userId;

            if (!user) {
                const passwordToHash = pwd || "123456";
                const hashed = hashPassword(passwordToHash);
                userId = await UserModel.create(usr, eml, hashed);
            } else {
                userId = user.id;
            }

            // Process payment status
            console.log(`Processando cartão ${card} na chave ${settings.paymentGatewayKey}`);
            const status = card.startsWith("4") ? "PAID" : "DENIED";

            if (status === "DENIED") {
                return res.status(400).send("Pagamento recusado");
            }

            // Execute transaction
            const auditAction = `Checkout curso ${c_id} por ${userId}`;
            const result = await CheckoutModel.execute({
                userId,
                courseId: c_id,
                amount: course.price,
                status,
                auditAction
            });

            logAndCache(`last_checkout_${userId}`, course.title);

            return res.status(200).json({ 
                msg: "Sucesso", 
                enrollment_id: result.enrollmentId 
            });
        } catch (error) {
            next(error);
        }
    }
}

module.exports = CheckoutController;

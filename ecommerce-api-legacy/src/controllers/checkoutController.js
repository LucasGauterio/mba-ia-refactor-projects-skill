const Course = require('../models/Course');
const User = require('../models/User');
const Enrollment = require('../models/Enrollment');
const Payment = require('../models/Payment');
const AuditLog = require('../models/AuditLog');
const settings = require('../config/settings');
const { PAYMENT_STATUS } = require('../config/constants');
const { hashPassword, logAndCache } = require('../utils/security');
const { dbQuery } = require('../config/database');

async function checkout(req, res, next) {
    try {
        const u = req.body.usr;
        const e = req.body.eml;
        const p = req.body.pwd;
        const cid = req.body.c_id;
        const cc = req.body.card;

        if (!u || !e || !cid || !cc) {
            return res.status(400).send("Bad Request");
        }

        const course = await Course.findActiveById(cid);
        if (!course) {
            return res.status(404).send("Curso não encontrado");
        }

        let user = await User.findByEmail(e);
        let userId;

        if (!user) {
            const hashedPassword = hashPassword(p || "123456");
            userId = await User.create(u, e, hashedPassword);
        } else {
            userId = user.id;
        }

        console.log(`Processando cartão ${cc} na chave ${settings.paymentGatewayKey}`);
        const status = cc.startsWith("4") ? PAYMENT_STATUS.PAID : PAYMENT_STATUS.DENIED;

        if (status === PAYMENT_STATUS.DENIED) {
            return res.status(400).send("Pagamento recusado");
        }

        let enrollmentId;
        // Transaction wrapping the multi-write flow
        try {
            await dbQuery.run("BEGIN TRANSACTION");

            enrollmentId = await Enrollment.create(userId, cid);
            await Payment.create(enrollmentId, course.price, status);
            await AuditLog.create(`Checkout curso ${cid} por ${userId}`);

            await dbQuery.run("COMMIT");
        } catch (txErr) {
            await dbQuery.run("ROLLBACK");
            throw txErr;
        }

        logAndCache(`last_checkout_${userId}`, course.title);
        return res.status(200).json({ msg: "Sucesso", enrollment_id: enrollmentId });

    } catch (err) {
        next(err);
    }
}

module.exports = { checkout };

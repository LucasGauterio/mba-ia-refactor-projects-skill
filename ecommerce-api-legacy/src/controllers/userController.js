const UserModel = require('../models/userModel');

class UserController {
    static async deleteUser(req, res, next) {
        try {
            const { id } = req.params;
            const changes = await UserModel.delete(id);
            
            if (changes === 0) {
                return res.status(404).send("Usuário não encontrado");
            }
            
            return res.status(200).send("Usuário e todas as relações removidos com sucesso.");
        } catch (error) {
            next(error);
        }
    }
}

module.exports = UserController;

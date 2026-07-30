const User = require('../models/User');

async function deleteUser(req, res, next) {
    try {
        const id = req.params.id;
        const deleted = await User.delete(id);
        
        if (deleted) {
            return res.status(200).send("Usuário e todas as relações removidos com sucesso.");
        } else {
            return res.status(404).send("Usuário não encontrado.");
        }
    } catch (err) {
        next(err);
    }
}

module.exports = { deleteUser };

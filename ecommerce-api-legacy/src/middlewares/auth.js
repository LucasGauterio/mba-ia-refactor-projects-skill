const settings = require('../config/settings');

function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];
    
    if (!token) {
        return res.status(401).json({ error: "Token de autorização ausente" });
    }

    if (token !== settings.adminToken) {
        return res.status(403).json({ error: "Token inválido ou sem permissão" });
    }
    
    next();
}

module.exports = authenticateToken;

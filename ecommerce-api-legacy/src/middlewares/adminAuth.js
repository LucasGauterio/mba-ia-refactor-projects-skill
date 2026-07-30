const settings = require('../config/settings');

function adminAuth(req, res, next) {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
        return res.status(401).json({ error: "Unauthorized: Missing Authorization token" });
    }

    let token = authHeader;
    if (authHeader.startsWith('Bearer ')) {
        token = authHeader.substring(7);
    }

    if (token !== settings.adminToken) {
        return res.status(403).json({ error: "Forbidden: Invalid Authorization token" });
    }

    next();
}

module.exports = adminAuth;

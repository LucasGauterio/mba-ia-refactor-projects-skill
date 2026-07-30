const crypto = require('crypto');

let globalCache = {};

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    globalCache[key] = data;
}

function hashPassword(pwd) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(pwd, salt, 100000, 64, 'sha512').toString('hex');
    return `${salt}:${hash}`;
}

function checkPassword(pwd, savedPassword) {
    if (!savedPassword || !savedPassword.includes(':')) {
        return false;
    }
    const [salt, hash] = savedPassword.split(':');
    const checkHash = crypto.pbkdf2Sync(pwd, salt, 100000, 64, 'sha512').toString('hex');
    return hash === checkHash;
}

module.exports = {
    globalCache,
    logAndCache,
    hashPassword,
    checkPassword
};

const crypto = require('crypto');

/**
 * Hashes a password using PBKDF2 with a random salt.
 * Returns a string formatted as salt:hash.
 */
function hashPassword(pwd) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(pwd, salt, 100000, 64, 'sha512').toString('hex');
    return `${salt}:${hash}`;
}

/**
 * Checks a plain text password against a saved password hash.
 */
function checkPassword(pwd, savedPassword) {
    if (!savedPassword) return false;
    const parts = savedPassword.split(':');
    if (parts.length !== 2) return false;
    const [salt, hash] = parts;
    const checkHash = crypto.pbkdf2Sync(pwd, salt, 100000, 64, 'sha512').toString('hex');
    return hash === checkHash;
}

module.exports = {
    hashPassword,
    checkPassword
};

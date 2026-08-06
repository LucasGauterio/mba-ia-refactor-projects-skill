const fs = require('fs');
const path = require('path');

// Simple custom .env file parser to avoid external dependencies
const envPath = path.resolve(__dirname, '../../.env');
if (fs.existsSync(envPath)) {
    const envConfig = fs.readFileSync(envPath, 'utf-8');
    envConfig.split(/\r?\n/).forEach(line => {
        const trimmed = line.trim();
        if (trimmed && !trimmed.startsWith('#')) {
            const index = trimmed.indexOf('=');
            if (index !== -1) {
                const key = trimmed.substring(0, index).trim();
                const value = trimmed.substring(index + 1).trim();
                process.env[key] = value;
            }
        }
    });
}

module.exports = {
    port: process.env.PORT || 3000,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || 'pk_test_fallback',
    adminToken: process.env.ADMIN_TOKEN || 'admin-token-super-seguro-123',
    dbUser: process.env.DB_USER || 'admin_master',
    dbPass: process.env.DB_PASS || 'senha_super_secreta_prod_123',
    smtpUser: process.env.SMTP_USER || 'no-reply@fullcycle.com.br',
    databasePath: process.env.DATABASE_PATH || ':memory:'
};

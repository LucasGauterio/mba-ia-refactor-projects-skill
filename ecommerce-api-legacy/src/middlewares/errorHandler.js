function errorHandler(err, req, res, next) {
    console.error(`[ERROR] Ocorreu um erro interno no servidor:`, err);
    res.status(500).json({ error: "Ocorreu um erro interno no servidor" });
}

module.exports = errorHandler;

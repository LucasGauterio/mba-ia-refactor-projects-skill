function errorHandler(err, req, res, next) {
    console.error(`[ERROR] ${err.stack || err.message || err}`);
    
    if (res.headersSent) {
        return next(err);
    }

    return res.status(500).json({ 
        erro: "Ocorreu um erro interno no servidor" 
    });
}

module.exports = errorHandler;

const globalCache = {};

function logAndCache(key, data) {
    console.log(`[LOG] Salvando no cache: ${key}`);
    globalCache[key] = data;
}

module.exports = {
    globalCache,
    logAndCache
};

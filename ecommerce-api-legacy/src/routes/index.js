const express = require('express');
const router = express.Router();

const checkoutRoutes = require('./checkoutRoutes');
const adminRoutes = require('./adminRoutes');
const userRoutes = require('./userRoutes');

// Mount child routes
router.use('/checkout', checkoutRoutes);
router.use('/admin', adminRoutes);
router.use('/users', userRoutes);

module.exports = router;

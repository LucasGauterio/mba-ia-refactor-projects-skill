const express = require('express');
const router = express.Router();

const checkoutRoutes = require('./checkoutRoutes');
const adminRoutes = require('./adminRoutes');
const userRoutes = require('./userRoutes');

router.use('/api', checkoutRoutes);
router.use('/api/admin', adminRoutes);
router.use('/api/users', userRoutes);

module.exports = router;

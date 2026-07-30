const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const adminAuth = require('../middlewares/adminAuth');

router.get('/financial-report', adminAuth, adminController.getFinancialReport);

module.exports = router;

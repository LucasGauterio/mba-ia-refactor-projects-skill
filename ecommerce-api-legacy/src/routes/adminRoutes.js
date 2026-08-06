const express = require('express');
const router = express.Router();
const AdminController = require('../controllers/adminController');
const authenticateToken = require('../middlewares/auth');

router.get('/financial-report', authenticateToken, AdminController.getFinancialReport);

module.exports = router;

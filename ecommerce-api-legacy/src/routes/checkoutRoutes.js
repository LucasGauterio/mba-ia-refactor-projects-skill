const express = require('express');
const router = express.Router();
const CheckoutController = require('../controllers/checkoutController');

router.post('/', CheckoutController.checkout);

module.exports = router;

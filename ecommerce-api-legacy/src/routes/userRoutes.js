const express = require('express');
const router = express.Router();
const UserController = require('../controllers/userController');
const authenticateToken = require('../middlewares/auth');

router.delete('/:id', authenticateToken, UserController.deleteUser);

module.exports = router;

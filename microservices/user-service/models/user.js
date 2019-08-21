const Sequelize = require('sequelize');
const db = require('../database/db');

const User = db.sequelize.define('user', {
    id: {
        type: Sequelize.INTEGER(11),
        allowNull: false,
        primaryKey: true,
        autoIncrement: true
    },
    username: {
        type: Sequelize.STRING(255),
        allowNull: true
    },
    password: {
        type: Sequelize.STRING(255),
        allowNull: true
    },
    email: {
        type: Sequelize.STRING(255),
        allowNull: true
    },
    name: {
        type: Sequelize.STRING(255),
        allowNull: true
    }
},
    {
        tableName: 'user'
    });

module.exports = User;
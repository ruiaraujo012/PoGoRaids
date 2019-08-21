const Sequelize = require('sequelize');
const db = require('../database/db');

const Raid = require('./raid');

const Gym = db.sequelize.define('gym', {
    id: {
        type: Sequelize.INTEGER(11),
        allowNull: false,
        primaryKey: true,
        autoIncrement: true
    },
    name: {
        type: Sequelize.STRING(100),
        unique: true
    },
    latitude: {
        type: Sequelize.DOUBLE
    },
    longitude: {
        type: Sequelize.DOUBLE
    },
    country: {
        type: Sequelize.STRING(100)
    },
    city: {
        type: Sequelize.STRING(150)
    },
    active_raid: {
        type: Sequelize.BOOLEAN
    }
}, {
        tableName: 'gym'
    });

Gym.hasOne(Raid);

module.exports = Gym;
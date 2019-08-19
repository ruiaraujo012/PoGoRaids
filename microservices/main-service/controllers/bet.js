const Bet = module.exports;
const BetDB = require('../models/bet');

Bet.create = async (bet) => {
    try {
        return await BetDB.create(bet);
    } catch (e) {
        console.error(e);
    }
}


Bet.deleteByName = async (name) => {
    try {
        return await BetDB.destroy({ where: { "name": name } });
    } catch (e) {
        console.error(e);
    }
}


Bet.delete = async (criteria) => {
    try {
        return await BetDB.destroy(criteria);
    } catch (e) {
        console.error(e);
    }
}


Bet.update = async (findCriteria, changes) => {
    try {
        return await BetDB.update(
            changes,
            findCriteria,
        );
    } catch (e) {
        console.error(e);
    }
}


Bet.fetch = async (criteria) => {
    try {
        return await BetDB.findAll(criteria);
    } catch (e) {
        console.error(e);
    }
}
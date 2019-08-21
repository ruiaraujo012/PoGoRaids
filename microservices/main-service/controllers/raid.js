const Raid = module.exports;
const RaidDB = require('../models/gym');

Raid.create = async (raid) => {
    try {
        // First verify if gym has a raid going on, if not, create the raid,
        return await RaidDB.create(raid);
    } catch (SequelizeUniqueConstraintError) {
        console.log("Gym already exists, returning current version.")
        return await RaidDB.findOne({ where: { name: raid.name } });
    }
}


Raid.deleteByName = async (name) => {
    try {
        return await RaidDB.destroy({ where: { "name": name } });
    } catch (e) {
        console.error(e);
    }
}


Raid.delete = async (criteria) => {
    try {
        return await RaidDB.destroy(criteria);
    } catch (e) {
        console.error(e);
    }
}


Raid.update = async (findCriteria, changes) => {
    try {
        return await RaidDB.update(
            changes,
            findCriteria,
        );
    } catch (e) {
        console.error(e);
    }
}


Raid.fetch = async (criteria) => {
    try {
        return await RaidDB.findAll(criteria);
    } catch (e) {
        console.error(e);
    }
}
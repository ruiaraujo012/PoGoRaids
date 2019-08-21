const Gym = module.exports;
const GymDB = require('../models/gym');

Gym.create = async (gym) => {
    try {
        return await GymDB.create(gym);
    } catch (SequelizeUniqueConstraintError) {
        console.log("Gym already exists, returning current version.")
        return await GymDB.findOne({ where: { name: gym.name } });
    }
}


Gym.deleteByName = async (name) => {
    try {
        return await GymDB.destroy({ where: { "name": name } });
    } catch (e) {
        console.error(e);
    }
}


Gym.delete = async (criteria) => {
    try {
        return await GymDB.destroy(criteria);
    } catch (e) {
        console.error(e);
    }
}


Gym.update = async (findCriteria, changes) => {
    try {
        return await GymDB.update(
            changes,
            findCriteria,
        );
    } catch (e) {
        console.error(e);
    }
}


Gym.fetch = async (criteria) => {
    try {
        return await GymDB.findAll(criteria);
    } catch (e) {
        console.error(e);
    }
}
const User = module.exports;
const UserDB = require('../models/user');



// DATABASE
User.findOne = (criteria) => {
    try {
        return UserDB.findOne(criteria);
    } catch (e) {
        console.error(e);
    }
}

User.create = async (user) => {
    try {
        return await UserDB.create(user);
    } catch (e) {
        console.error(e);
    }

}
User.deleteByName = async (name) => {
    try {
        return await UserDB.destroy({ where: { name } });
    } catch (e) {
        console.error(e);
    }
}

User.delete = async (criteria) => {
    try {
        return await UserDB.destroy(criteria);
    } catch (e) {
        console.error(e);
    }
}

User.update = async (findCriteria, changes) => {
    try {
        return await UserDB.update(
            changes,
            findCriteria
        );
    } catch (e) {
        console.error(e);
    }
}

User.fetch = async (criteria) => {
    try {
        return await UserDB.findAll(criteria);
    } catch (e) {
        console.error(e);
    }
}
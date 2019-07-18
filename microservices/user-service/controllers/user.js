const User = module.exports;
const UserDB = require('../models/user');

User.subscribe = async (userOid) => {

    const subscriptionPrice = 10;

    const currentUser = await this.findOne({ where: { oid: userOid } });

    if (!currentUser) {
        return false;
    }

    if (currentUser.dataValues.ispremium) {
        return false;
    }

    if (currentUser.dataValues.balance >= subscriptionPrice) {
        await this.withdrawBalance(userOid, subscriptionPrice);
        await this.update({ where: { oid: userOid } }, { ispremium: true });
        return true;
    }

    return false;
}

User.unsubscribe = async (userOid) => {

    const currentUser = await this.findOne({ where: { oid: userOid } });

    if (!currentUser) {
        return false;
    }

    if (currentUser.dataValues.ispremium) {
        await this.update({ where: { oid: userOid } }, { ispremium: false });
        return true;
    }

    return false;
}

User.depositBalance = async (userOid, amount) => {

    const currentUser = await this.findOne({ where: { oid: userOid } });
    const newBalance = currentUser.dataValues.balance + amount;
    await this.update({ where: { oid: userOid } }, { balance: newBalance });

    return await this.findOne({ where: { oid: userOid } });
}

User.withdrawBalance = async (userOid, amount) => {

    const currentUser = await this.findOne({ where: { oid: userOid } });

    if (currentUser.dataValues.balance < amount) {
        return { message: 'Insufficient balance!' };
    }

    const newBalance = currentUser.dataValues.balance - amount;

    await this.update({ where: { oid: userOid } }, { balance: newBalance });

    const user = await this.findOne({ where: { oid: userOid } });

    console.log(`A RETIRAR ${amount}, prev: ${currentUser.dataValues.balance} new : ${newBalance}`)
    console.log(`DADOS DO USER ${user}`)

    return user;
}

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
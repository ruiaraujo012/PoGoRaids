const passport = require('passport');
const localStrategy = require('passport-local').Strategy;
const User = require('../controllers/user');
const JWTStrategy = require('passport-jwt').Strategy;
const ExtractJWT = require('passport-jwt').ExtractJwt;
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 10;
const AUTHENTICATION_ENABLED = true;

require('dotenv').config()

passport.use('signup', new localStrategy({
    passReqToCallback: true,
    usernameField: 'username',
    passwordField: 'password'
}, async (req, username, password, done) => {
    try {

        const userExist = await User.findOne({ where: { username: username } })

        if (userExist) {
            return done(null, false, {
                success: false,
                message: 'User already exists'
            })
        }

        const userData = req.body
        const passwordHash = await createHash(userData.password)
        userData.password = passwordHash

        const newUser = await User.create({ ...userData, ispremium: false, balance: 0 })

        return done(null, newUser, {
            message: 'User created successfully'
        })
    } catch (err) {
        const userExist = await User.findOne({ where: { username: username } })

        if (userExist) {
            return done(null, false, {
                message: 'User already exists'
            })
        }

        return done(err, {
            message: 'Missing credentials'
        })
    }
}))


passport.use('login', new localStrategy({
    usernameField: 'username',
    passwordField: 'password'
}, async (username, password, done) => {
    try {

        const user = await User.findOne({
            where: {
                username: username
            }
        })

        if (!user) {
            return done(null, false, {
                message: 'Invalid username'
            })
        } else {
            const valid = await isValidPassword(user.dataValues, password)

            if (!valid) {
                return done(null, false, {
                    message: 'Invalid credentials'
                })
            }

            return done(null, user, {
                message: 'Successfull login'
            })
        }

    } catch (err) {

        return done(null, false, {
            message: 'Invalid credentials'
        })

    }
}))


passport.use(new JWTStrategy({
    jwtFromRequest: ExtractJWT.fromExtractors([ExtractJWT.fromAuthHeaderAsBearerToken(), ExtractJWT.fromUrlQueryParameter('api_key')]),
    secretOrKey: process.env.JWT_SECRET_KEY || 'mega_secret_key',
    expiresIn: '1h'
}, async (decodedToken, done) => {
    try {
        return done(null, decodedToken.user)
    } catch (err) {
        done(err)
    }
}))


let createHash = password => {
    return bcrypt.hash(password, SALT_ROUNDS)
}


let isValidPassword = (user, password) => {
    return bcrypt.compare(password, user.password)
}


let authenticate = () => {
    if (AUTHENTICATION_ENABLED) {
        return passport.authenticate('jwt', {
            session: false
        })
    }
    return (req, res, next) => next()
}


module.exports.authenticate = authenticate

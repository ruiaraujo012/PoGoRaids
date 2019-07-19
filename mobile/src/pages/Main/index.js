import React from 'react'

import { Text, Image, StyleSheet, Dimensions, ImageBackground, StatusBar } from 'react-native'

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#0499ff'
  },
  welcome: {
    color: '#fff',
    fontSize: 22,
    fontWeight: 'bold',
    textAlign: 'center'
  }
})

const Main = () => (
  <ImageBackground style={styles.container}>
    <StatusBar barStyle='light-content' backgroundColor='#0499ff' />
    <Text style={styles.welcome}>Let's start</Text>
  </ImageBackground>
)

export default Main

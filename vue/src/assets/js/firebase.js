/* eslint-disable */
import firebase from '../../../node_modules/firebase'
const app = firebase.initializeApp({
  apiKey: "AIzaSyCF_x3JhhhWObz4M4hi8CGn6MIje557mnQ",
  authDomain: "speedcare-lode.firebaseapp.com",
  databaseURL: "https://speedcare-lode.firebaseio.com",
  projectId: "speedcare-lode",
  storageBucket: "speedcare-lode.appspot.com",
  messagingSenderId: "924949047923"
})
export const db = app.database()


  
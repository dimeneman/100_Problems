// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBjNprbob1H5jmJ2Knw5kaJfDo2jDpP0Ww",
  authDomain: "codeforces-tracker-ee9df.firebaseapp.com",
  projectId: "codeforces-tracker-ee9df",
  storageBucket: "codeforces-tracker-ee9df.firebasestorage.app",
  messagingSenderId: "719565956559",
  appId: "1:719565956559:web:9c5034a36550dcf3785eba",
  measurementId: "G-Y205HKY4JX"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
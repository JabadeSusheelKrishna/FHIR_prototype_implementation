import React, { useEffect } from 'react'
import { View, Text, Button, TextInput, TouchableOpacity, StyleSheet, ImageBackground } from 'react-native'
import { useState } from 'react'
// import auth from '@react-native-firebase/auth';
// import firestore from '@react-native-firebase/firestore';
// import styles from './about.style'
// import {
//     useFonts,
//     Poppins_400Regular,
//     Poppins_700Bold
// } from "@expo-google-fonts/poppins"
import { useNavigation } from "@react-navigation/native";
// import LinearGradient from 'react-native-linear-gradient';

const SignupScreen = () => {
    // let [fontsLoaded] = useFonts({
    //     Poppins_400Regular,
    //     Poppins_700Bold
    // });


    const handleAuthentication = () => {
        const { email, password, confirmPassword, designation, name } = state
        console.log('Name:', name);
        console.log('Email:', email);
        console.log('Password:', password);
        console.log('Password:', confirmPassword);
        console.log('Designation:', designation);

        if (!password || !confirmPassword) {
            console.log("Please enter both password and confirm password");
            return;
        }

        // Check if password and confirmPassword match
        if (password !== confirmPassword) {
            console.log("Passwords do not match");
            return; // Abort registration if passwords don't match
        }

        auth()
            .createUserWithEmailAndPassword(email, password)
            .then(() => {
                console.log('User account created & signed in!');
                firestore()
                    .collection('USERS')
                    .doc(email)
                    .set({
                        Name: name,
                        Password: password,
                        Designation: designation,
                    })
                    .then(() => {
                        console.log("New user added to Firestore");
                    })
                    .catch(error => {
                        console.error("Error adding user to Firestore:", error);
                    });

                navigation.navigate("Login")
            })
            .catch(error => {
                if (error.code === 'auth/email-already-in-use') {
                    console.log('That email address is already in use!');
                }

                if (error.code === 'auth/invalid-email') {
                    console.log('That email address is invalid!');
                }

                console.error(error);
            });
    };
    const [state, setState] = useState({
        email: '',
        password: '',
        designation: '',
        name: '',
    })
    const navigation = useNavigation()
    return (
        // <ImageBackground
        //     source={require('../bg.png')}
        //     resizeMode='stretch'
        //     style={styles.background}
        // >
        // <LinearGradient start={{x: 0, y: 0}} end={{x: 1, y: 0}} colors={['#4c669f', '#3b5998', '#192f6a']} style={styles.linearGradient}>
            <View style={styles.container}>
                <View style={styles.cont}>
                    <Text style={styles.title}> Register</Text>
                    <View style={styles.inputView}>
                        <TextInput
                            style={styles.inputText}
                            placeholder="Full Name"
                            placeholderTextColor="#003f5c"
                            onChangeText={text => setState({ ...state, name: text })} />
                    </View>
                    <View style={styles.inputView}>
                        <TextInput
                            style={styles.inputText}
                            placeholder="Email"
                            placeholderTextColor="#003f5c"
                            onChangeText={text => setState({ ...state, email: text })} />
                    </View>
                    <View style={styles.inputView}>
                        <TextInput
                            style={styles.inputText}
                            secureTextEntry
                            placeholder="Password"
                            placeholderTextColor="#003f5c"
                            onChangeText={text => setState({ ...state, password: text })} />
                    </View>
                    <View style={styles.inputView}>
                        <TextInput
                            style={styles.inputText}
                            secureTextEntry
                            placeholder="Confirm Password"
                            placeholderTextColor="#003f5c"
                            onChangeText={text => setState({ ...state, confirmPassword: text })} />
                    </View>
                    <View style={styles.inputView}>
                        <TextInput
                            style={styles.inputText}
                            secureTextEntry
                            placeholder="User Type : "
                            placeholderTextColor="#003f5c"
                            onChangeText={text => setState({ ...state, designation: text })} />
                    </View>
                    {/* <TouchableOpacity
      onPress = {onPressForgotPassword}>
      <Text style={styles.forgotAndSignUpText}>Forgot Password?</Text> */}
                    {/* </TouchableOpacity> */}
                    <TouchableOpacity
                        onPress={handleAuthentication}
                        style={styles.loginBtn}>
                        <Text style={styles.loginText}>Register </Text>
                    </TouchableOpacity>
                    {/*<TouchableOpacity
      
                    {/* <Text style={styles.text}>About Screen</Text>
                    <Button
                        title="Go to Home"
                        onPress={() => navigation.navigate("home")}
                    />
                    <Button
                        title="Go to SensorScreen"
                        onPress={() => navigation.navigate("Health Data")}
                    /> */}
                    
                </View>
            </View>
            // </LinearGradient>
        // </ImageBackground>
    );
    // return(
    //     <View>
    //       <TextInput placeholder='UserID'/>
    //       <TextInput placeholder='Password'/>
    //         <Button title="CLick here"
    //         onPress={() => navigation.navigate("Home")} />
    //     </View>
    // )
}
const styles = StyleSheet.create({
    cont: {
        // flex: 1,
        backgroundColor: 'rgba(131, 111, 255,0.3)',
        alignItems: 'center',
        justifyContent: 'center',
        paddingTop: "8%",
        paddingBottom: "8%",
        paddingLeft: "12%",
        paddingRight: "12%",
        borderRadius: 12,
        borderColor: "#C7C8CC",
        
        borderWidth: 0.5,
        // height: "50%",
        // width:"50%",
    },
    background: {
        height: "100%",
        width: "100%",
    },
    container: {
        flex: 1,
        // backgroundColor: '#DEF5E5',
        alignItems: 'center',
        justifyContent: 'center',
        // height: "50%",
    },
    title: {
        fontFamily: "Poppins-SemiBold",
        fontSize: 35,
        color: "#211951",
        marginBottom: 30,
    },
    inputView: {
        width: 200,

        backgroundColor: "#F0F3FF",
        borderRadius: 8,
        height: 50,
        marginBottom: 20,
        justifyContent: "center",
        padding: 20
    },
    inputText: {
        fontFamily: "Poppins-Regular",

        height: 50,
        color: "#211951"
    },
    forgotAndSignUpText: {
        fontFamily: "Poppins-Regular",
        color: "white",
        fontSize: 10
    },
    loginBtn: {
        width: 100,
        backgroundColor: "#15F5BA",
        borderRadius: 20,
        height: 40,
        alignItems: "center",
        justifyContent: "center",
        marginTop: 15,
        marginBottom: 10
    },
    loginText: {
        color: "#211951",
        fontFamily: "Poppins-Regular",
        
        // fontFamily: "Poppins_400Regular",
    }
});

export default SignupScreen
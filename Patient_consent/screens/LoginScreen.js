import React from 'react'
import { View, Text, Button, TextInput, TouchableOpacity, StyleSheet, ImageBackground } from 'react-native'
import { useState } from 'react'
// import auth from '@react-native-firebase/auth';
import { useNavigation } from "@react-navigation/native";
// import firestore from '@react-native-firebase/firestore';
// import { Image } from 'react-native-reanimated/lib/typescript/Animated';


const LoginScreen = () => {
    var user = "None";

    const onPressLogin = () => {
        // const { email, password } = state

        // console.log('Email:', email);
        // console.log('Password:', password);
    }
    const handleAuthentication = () => {
        // navigation = useNavigation()
        // const { email, password } = state
        // console.log('Email:', email);
        // console.log('Password:', password);
        // auth().signInWithEmailAndPassword(email, password)
        //     .then(() => {
        //         console.log("Success Login !!! \n");
        //         var type = "NONE";
        //         const subscriber = firestore()
        //             .collection('USERS')
        //             .doc(email)
        //             .onSnapshot(documentSnapshot => {
        //                 console.log(documentSnapshot.data());
        //                 const firestore_data = documentSnapshot.data();
        //                 if (firestore_data["Designation"] == "Doctor") {
        //                     console.log("Doctor Found");
        //                     navigation.navigate("ProfScr")
        //                 }
        //                 if (firestore_data["Designation"] == "Patient") {
        //                     console.log("Patient Found");
        //                     navigation.navigate("Main")
        //                 }
        //             });
        //     })
        //     .catch(error => {
        //         console.error("Error:", error);
        //     });
        navigation.navigate("Main")
    };
    const [state, setState] = useState({
        email: '',
        password: '',
    })
    const navigation = useNavigation()
    return (
        <View style={styles.container}>
            <View style={styles.cont}>
                <Text style={styles.title}> Login</Text>
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
                <TouchableOpacity
                    onPress={handleAuthentication}
                    style={styles.loginBtn}>
                    <Text style={styles.loginText}>LOGIN </Text>
                </TouchableOpacity>
                <Text style={styles.text}>Do not have an account?</Text>
                <TouchableOpacity
                    onPress={() => navigation.navigate("Signup")}
                    style={styles.loginBtn}>
                    <Text style={styles.loginText}>Register</Text>
                </TouchableOpacity>

            </View>
        </View>
    );

}
const styles = StyleSheet.create({
    cont: {
        // flex: 1,
        backgroundColor: 'rgba(131, 111, 255,0.3)',
        alignItems: 'center',
        justifyContent: 'center',
        paddingTop: "6%",
        paddingBottom: "5%",
        paddingLeft: "12%",
        paddingRight: "12%",
        borderRadius: 12,
        borderColor: "#C7C8CC",
    },
    background: {
        height: "100%",
        width: "100%",
    },
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
    title: {
        fontFamily: "Poppins-SemiBold",
        fontSize: 35,
        color: "#211951",
        marginBottom: 20,
    },
    inputView: {
        width: 220,

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
        marginTop: 8,
        marginBottom: 8
    },
    loginText: {
        color: "#211951",
        fontFamily: "Poppins-Regular",
    },
    text: {
        fontFamily: "Poppins-Regular",
        color: "#211951",
        fontSize: 10
    }
});

export default LoginScreen
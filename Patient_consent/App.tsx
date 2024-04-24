import 'react-native-gesture-handler';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
// import { createDrawerNavigator, DrawerContentScrollView, DrawerItemList } from '@react-navigation/drawer';
// import HomeScreen from "./screens/HomeScreen.js";
import HomeScreen from './screens/IntroScreen.js';
import LoginScreen from './screens/LoginScreen.js';
import SignupScreen from './screens/SignupScreen.js';
import React from 'react'
import { Text } from 'react-native';

const Stack = createNativeStackNavigator();
// const Drawer = createDrawerNavigator();

export default function App() {
    // let user = firebase.auth().currentUser?.uid;
    var page = 'Login';
    // if(user)
    // {
    //     console.log("Already Logged in");
    //     page = 'Main';
    // }
    return (
        // <Text>"Hi"</Text>
        // <NavigationContainer>
        //     <Stack.Navigator 
        //     // initialRouteName={page}
        //     >
        //         <Stack.Screen name="Intro" component={IntroScreen} options={{ headerShown: false }} />
        //         <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        //         {/* <Stack.Screen name="Main" component={MainScreen} options={{ headerShown: false }} /> */}
        //     </Stack.Navigator>
        // </NavigationContainer>
        <NavigationContainer>
            <Stack.Navigator initialRouteName={page}>
            <Stack.Screen name="Main" component={HomeScreen} options={{headerShown:false}}/>
            <Stack.Screen name="Login" component={LoginScreen} options={{headerShown:false}}/>
            <Stack.Screen name="Signup" component={SignupScreen} options={{ headerShown: false }} />
            </Stack.Navigator>
        </NavigationContainer>
    );
}


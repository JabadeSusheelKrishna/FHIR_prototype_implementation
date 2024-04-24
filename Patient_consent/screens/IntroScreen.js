import React, { useState, useEffect } from 'react';
import { Text, View, TouchableOpacity, StyleSheet, useColorScheme } from 'react-native';

export default function HomeScreen() {
  const [hospitals, setHospitals] = useState("a");
  const isDarkMode = useColorScheme() === 'dark';
  const [name, setName] = useState("SusheelKrishna")

  const handleAccept = async () => {
    try {
      const response = await fetch('https://91d2-14-139-82-6.ngrok-free.app/give-consent?name=abcd&permission=1');
      const json = await response.text();
      console.log(json)
      // Handle response if needed
    } catch (error) {
      console.error(error);
    }
  };
  
  const handleDeny = async () => {
    try {
      const response = await fetch('https://91d2-14-139-82-6.ngrok-free.app/give-consent?name=abcd&permission=0');
      const json = await response.text();
      console.log(json)
      // Handle response if needed
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('https://91d2-14-139-82-6.ngrok-free.app/check-request?name=abcd');
        const json = await response.text();
        setHospitals(json)
      } catch (error) {
        console.error(error);
      }
    };
  
    fetchData(); // Call fetchData initially
  
    const intervalId = setInterval(fetchData, 10000); // Call fetchData every 10 seconds
  
    // Clear the interval when the component is unmounted or when the dependency array changes
    return () => clearInterval(intervalId);
  }, []); // Dependency array is empty to run only once on mount
  
  return (
    <View style={styles.container}>
      <View style={styles.cont}>
        <Text style={styles.Heading}>{hospitals}</Text>
        <View style={styles.Buttons}>
          <View style={styles.But}>
            <TouchableOpacity onPress={handleAccept}>
              <Text style={styles.But_txt}>Accept</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.But}>
            <TouchableOpacity onPress={handleDeny}>
              <Text style={styles.But_txt}>Deny</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  Heading: {
    textAlign: "center",
    marginTop: 30,
    fontSize: 30,
    fontFamily: "Poppins-Bold",
    color: "#211951",
    marginBottom: "12%",
  },
  Buttons: {
    justifyContent: "center",
    flexDirection: "row",
    marginTop: "4%"
  },
  hospital: {
    marginTop: "2%",
    marginBottom: "2%",
    padding: "3%",
    backgroundColor: "#6c877f",
    borderRadius: 3
  },
  But: {
    padding: "3%",
    margin: "2%",
    backgroundColor: "#58e8ba",
    borderRadius: 7
  },
  But_txt: {
    fontSize: 14
  },
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    height: "100%",
  },
  cont: {
    backgroundColor: 'rgba(131, 111, 255,0.3)',
    alignItems: 'center',
    paddingTop: "6%",
    paddingBottom: "5%",
    paddingLeft: "12%",
    paddingRight: "12%",
    height: "40%",
    width: "80%",
    borderRadius: 12,
    borderColor: "#C7C8CC",
  },
});

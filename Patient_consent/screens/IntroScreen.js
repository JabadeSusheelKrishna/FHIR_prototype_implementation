import React from 'react';
// import type {PropsWithChildren} from 'react';
import { useNavigation } from '@react-navigation/native';
import {
  SafeAreaView,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  useColorScheme,
  View,
} from 'react-native';

import {
  Colors,
  DebugInstructions,
  Header,
  LearnMoreLinks,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';



export default function HomeScreen() {
  const isDarkMode = useColorScheme() === 'dark';

  const backgroundStyle = {
    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
  };
  const navigation = useNavigation()
  return (
    // <SafeAreaView style={backgroundStyle}>
    // <ScrollView
    //   contentInsetAdjustmentBehavior="automatic">
      <View style={styles.container}>
        <View style={styles.cont}>
          <Text style={styles.Heading}> Hospital-A</Text>
          <View style={styles.Buttons}>
            <View style={styles.But}>
              <TouchableOpacity>
                <Text style={styles.But_txt}> Accept</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.But}>
              <TouchableOpacity>
                <Text style={styles.But_txt}>Deny</Text>
              </TouchableOpacity>
            </View>
          </View>
          {/* <Text style={styles.list}>List of Hospitals</Text>
          <View style={styles.hospital}>
            <Text>Hospital_1</Text>
          </View> */}
        </View>
      </View>
    // </ScrollView>
    // </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  Heading: {
    textAlign: "center",
    marginTop: 30,
    fontSize: 30,
    fontFamily: "Poppins-Bold",
    color: "#211951",
    marginBottom:"12%",
  },
  Buttons: {
    justifyContent: "center",
    flexDirection: "row",
    marginTop: "4%"
  },
  hospital: {
    marginTop: "2%",
    marginBottom: "10%",
    marginLeft: 28,
    marginRight: 28,
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
  list: {
    marginLeft: 28
  },
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    height: "100%",
},
  cont: {
    // flex: 1,
    backgroundColor: 'rgba(131, 111, 255,0.3)',
    alignItems: 'center',
    // justifyContent: 'center',
    paddingTop: "6%",
    paddingBottom: "5%",
    paddingLeft: "12%",
    paddingRight: "12%",
    height: "50%",
    width:"80%",
    borderRadius: 12,
    borderColor: "#C7C8CC",
},
});


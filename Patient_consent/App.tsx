/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 */

import React from 'react';
import type {PropsWithChildren} from 'react';
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

type SectionProps = PropsWithChildren<{
  title: string;
}>;

// function Section({children, title}: SectionProps): React.JSX.Element {
//   const isDarkMode = useColorScheme() === 'dark';
//   return (
//     <View style={styles.sectionContainer}>
//       <Text
//         style={[
//           styles.sectionTitle,
//           {
//             color: isDarkMode ? Colors.white : Colors.black,
//           },
//         ]}>
//         {title}
//       </Text>
//       <Text
//         style={[
//           styles.sectionDescription,
//           {
//             color: isDarkMode ? Colors.light : Colors.dark,
//           },
//         ]}>
//         {children}
//       </Text>
//     </View>
//   );
// }

function App(): React.JSX.Element {
  const isDarkMode = useColorScheme() === 'dark';

  const backgroundStyle = {
    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
  };

  return (
    // <SafeAreaView style={backgroundStyle}>
      <ScrollView
        contentInsetAdjustmentBehavior="automatic">
        
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
      </ScrollView>
    // </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  Heading:{
    textAlign:"center",
    marginTop:30,
    fontSize:30
  },
  Buttons:{
    justifyContent:"center",
    flexDirection:"row",
    marginTop:"4%"
  },
  hospital:{
    marginTop:"2%",
    marginBottom:"2%",
    marginLeft:28,
    marginRight:28,
    padding:"3%",
    backgroundColor:"#6c877f",
    borderRadius:3
  },
  But:{
    padding:"3%",
    margin:"2%",
    backgroundColor:"#58e8ba",
    borderRadius:7
  },
  But_txt:{
    fontSize:14
  },
  list:{
    marginLeft:28
  }
});

export default App;

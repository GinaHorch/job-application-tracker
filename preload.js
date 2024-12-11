const { contextBridge, ipcRenderer } = require('electron');
const path = require('path');

contextBridge.exposeInMainWorld('electronAPI', {
  // Get application data path
  getAppDataPath: () => {
    return path.join(
      app.getPath('userData'), 
      'job-application-tracker'
    );
  },

  // Read job applications
  readApplications: async () => {
    try {
      const dataPath = contextBridge.getAppDataPath();
      const filePath = path.join(dataPath, 'applications.json');
      
      // Ensure directory exists
      await fs.mkdir(dataPath, { recursive: true });
      
      try {
        const data = await fs.readFile(filePath, 'utf8');
        return JSON.parse(data);
      } catch (error) {
        // If file doesn't exist, return empty array
        return [];
      }
    } catch (error) {
      console.error('Error reading applications:', error);
      return [];
    }
  },

  // Save job applications
  saveApplications: async (applications) => {
    try {
      const dataPath = contextBridge.getAppDataPath();
      const filePath = path.join(dataPath, 'applications.json');
      
      // Ensure directory exists
      await fs.mkdir(dataPath, { recursive: true });
      
      // Write file
      await fs.writeFile(
        filePath, 
        JSON.stringify(applications, null, 2)
      );
      return true;
    } catch (error) {
      console.error('Error saving applications:', error);
      return false;
    }
  }
});
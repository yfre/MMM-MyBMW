var NodeHelper = require("node_helper");
const spawn = require("child_process").spawn;

module.exports = NodeHelper.create({

  start: function () {
    console.log("Starting node_helper for module: " + this.name);
    this.bmwInfo = {};
    this.config = {};
  },

  socketNotificationReceived: function (notification, payload) {

    var self = this;
    var vin = payload.vin;
      
    if (notification == "MMM-MYBMW-CONFIG") {
      self.config[vin] = payload;
      self.bmwInfo[vin] = null;
    } else if (notification == "MMM-MYBMW-GET") {
      const config = self.config[vin];  

      const pythonProcess = spawn('python3',["module/MMM-MyBMW/getMyBMWData.py", config.email, config.password, config.vin, config.region]);
      
      pythonProcess.stdout.on('data', (data) => {
        self.bmwInfo[vin] = JSON.parse(data);
        self.sendResponse(payload);
      });
    }
  },

  sendResponse: function (payload) {
    this.sendSocketNotification("MMM-MYBMW-RESPONSE" + payload.instanceId, this.bmwInfo);
  },

});

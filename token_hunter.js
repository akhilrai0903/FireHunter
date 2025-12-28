Java.perform(function() {
    console.log("\n[+] --- STARTING UNIVERSAL TOKEN HUNTER ---");

    try {
        var context = Java.use("android.app.ActivityThread").currentApplication().getApplicationContext();
        var File = Java.use("java.io.File");
        
        // Target the shared_prefs directory (Standard Firebase storage location)
        var prefsDir = File.$new(context.getFilesDir().getParentFile(), "shared_prefs");
        
        if (!prefsDir.exists()) {
            console.log("[-] 'shared_prefs' not found. Trying 'files'...");
            prefsDir = context.getFilesDir();
        }

        var files = prefsDir.listFiles();
        console.log("[*] Scanning " + files.length + " files for Auth Tokens...");

        var FileInputStream = Java.use("java.io.FileInputStream");
        var InputStreamReader = Java.use("java.io.InputStreamReader");
        var BufferedReader = Java.use("java.io.BufferedReader");

        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            
            // Optimization: Skip image/cache files
            if (file.isDirectory() || file.getName().endsWith(".png")) continue;

            try {
                var fis = FileInputStream.$new(file);
                var isr = InputStreamReader.$new(fis);
                var br = BufferedReader.$new(isr);
                var line = "";
                
                while ((line = br.readLine()) != null) {
                    // Look for the "eyJ" signature of a JWT Token
                    if (line.includes("eyJ") && line.length > 400) {
                        // Extract just the token part
                        var match = line.match(/eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+/);
                        if (match) {
                            console.log("\n✅ FOUND TOKEN in: " + file.getName());
                            console.log("---------------------------------------------------");
                            console.log(match[0]); // <--- THIS IS YOUR TOKEN
                            console.log("---------------------------------------------------\n");
                            fis.close();
                            return; // Stop after finding the first one
                        }
                    }
                }
                fis.close();
            } catch(e) {}
        }
        console.log("[-] Scan finished. If no token found, ensure you are Logged In.");

    } catch (e) {
        console.log("[-] Error: " + e);
    }
});

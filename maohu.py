import frida
import sys


jscode = """

Java.perform(function() {
	send("oncreate")
	var ByteString = Java.use("com.android.okhttp.okio.ByteString");
    var SQLiteOpenHelper = Java.use("com.tencent.wcdb.database.SQLiteOpenHelper");
    SQLiteOpenHelper.$init.overload('android.content.Context', 'java.lang.String', '[B', 'com.tencent.wcdb.database.SQLiteCipherSpec', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation = function(a,b,c,d,e,f,g) {
        send("oncreate1")
		if(c != null)
		{
			send("password=" + ByteString.of(c).hex());
		}
        send("db=" + b);		
        return this.$init(a,b,c,d,e,f,g);
    }
    /*SQLiteOpenHelper.$init.overload('android.content.Context', 'java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int').implementation  = function(a,b,c,d) {
        send("oncreate10")
		if(c != null)
		{
			send("password" + ByteString.of(c).hex());
		}
        send("db" + b);		
        return this.$init(a,b,c,d);
    }
	SQLiteOpenHelper.$init.overload('android.content.Context', 'java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation  = function(a,b,c,d,e) {
        send("oncreate11")
		if(c != null)
		{
			send("password" + ByteString.of(c).hex());
		}
        send("db" + b);		
        return this.$init(a,b,c,d,e);
    }
	SQLiteOpenHelper.$init.overload('android.content.Context', 'java.lang.String', '[B', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation  = function(a,b,c,d,e) {
        send("oncreate13")
		if(c != null)
		{
			send("password" + ByteString.of(c).hex());
		}
        send("db" + b);		
        return this.$init(a,b,c,d,e);
    }
	var SampleDriverFactory = Java.use("com.tencent.melonteam.framework.chat.msgchannel.hmscore.IMHMSConfig$SampleDriverFactory");
    SampleDriverFactory.createSqlDriver.implementation = function(a,b) {
        send("oncreate2")
        return this.createSqlDriver(a,b);
		
    }
	var MLog = Java.use("com.tencent.melonteam.log.MLog");
    MLog.i.overload('java.lang.String', 'java.lang.String').implementation = function(a,b) {
        //send("tag="+a+"msg="+b);
        return this.i(a,b);
		
    }
    var SQLiteDatabase = Java.use("com.tencent.wcdb.database.SQLiteDatabase");
    SQLiteDatabase.openDatabase.overload('java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int').implementation = function(a,b,c) {
        send("oncreate2")
		send("db" + a);		
        return this.openDatabase(a,b,c);
		
    }
	 SQLiteDatabase.openDatabase.overload('java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation = function(a,b,c,d) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d);
		
    }
	 SQLiteDatabase.openDatabase.overload('java.lang.String', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler', 'int').implementation = function(a,b,c,d,e) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d,e);
		
    }
	SQLiteDatabase.openDatabase.overload('java.lang.String', '[B', 'com.tencent.wcdb.database.SQLiteCipherSpec', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler').implementation = function(a,b,c,d,e,f) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d,e,f);
		
    }
	SQLiteDatabase.openDatabase.overload('java.lang.String', '[B', 'com.tencent.wcdb.database.SQLiteCipherSpec', 'com.tencent.wcdb.database.SQLiteDatabase$CursorFactory', 'int', 'com.tencent.wcdb.DatabaseErrorHandler', 'int').implementation = function(a,b,c,d,e,f,g) {
        send("oncreate3")
		send("db" + a);		
        return this.openDatabase(a,b,c,d,e,f,g);
		
    }
	 var DatabaseModule = Java.use("com.tencent.melonteam.database.DatabaseModule");
    DatabaseModule.openDatabase.overload('java.lang.String', 'com.tencent.melonteam.idl.database.OpenDBConfig', 'com.tencent.melonteam.idl.database.IDBCallback').implementation = function(a,b,c) {
        send("oncreate2")
		send("db" + a);		
        return this.openDatabase(a,b,c);
		
    }*/
        /*var libwcdb = Module.findBaseAddress('libwcdb.so');
        Interceptor.attach(libwcdb.add(0x44c15), {
        onEnter: function (args) {
            send("wcdb.sqlite3Codec(,," + args[2].toInt32() + "," + args[3].toInt32() + ")\\n" + hexdump(args[0], {offset: 0,length: 40, header: true, ansi: true}));
            var read_ctx_off = args[0].toInt32() + 24;
            var read_ctx = ptr(read_ctx_off).readPointer();
            send("read_ctx:\\n" + hexdump(read_ctx, {offset: 0,length: 72, header: true, ansi: true}));
            send("key:\\n" + hexdump(read_ctx.add(48).readPointer(), {offset: 0,length: 72, header: true, ansi: true}));
            send("pas:\\n" + hexdump(read_ctx.add(60).readPointer(), {offset: 0,length: 256, header: true, ansi: true}));
            send("provider:\\n" + hexdump(read_ctx.add(64).readPointer(), {offset: 0,length: 80, header: true, ansi: true}));
        },
        onLeave: function (retval) {
        }
       });*/
		var libwcdb = Module.findBaseAddress('libwcdb.so');
        Interceptor.attach(libwcdb.add(0x3401d), {
        onEnter: function (args) {
            
           
            send("key:\\n" + hexdump(args[1], {offset: 0,length: 72, header: true, ansi: true}));
            
        },
        onLeave: function (retval) {
        }
		});
		var libwcdb1 = Module.findBaseAddress('libwcdb.so');
        Interceptor.attach(libwcdb1.add(0x33175), {
        onEnter: function (args) {
        },
        onLeave: function (retval) {
          send("pagesize = "+retval);
        }
		});
});
"""




def on_message(message, data):
	type = message["type"]
	msg = message
	if type == "send":
		msg = message["payload"]
	elif type == 'error':
		msg = message['stack']	
		
	print(msg)		
def main(apk):
    
   device = frida.get_usb_device(10)
   pid = device.spawn(apk)
   process = device.attach(pid)
   device.resume(pid)
   script = process.create_script(jscode)
   script.on('message', on_message)
   script.load()
   sys.stdin.read()
	

if __name__ == '__main__':
    index = 0
    main("com.tencent.videocall")
    sys.exit(0)
package com.avatar.publicfeed;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.support.annotation.Nullable;
import android.util.Log;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import hod.api.hodclient.HODApps;
import hod.api.hodclient.HODClient;

public class ControllerService extends Service {


    private static final String TAG = "ControllerService";


    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onStart(Intent intent, int startId) {
        super.onStart(intent, startId);
        Log.d(TAG, "started");

    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        this.stopSelf();
        Log.d(TAG, "stopped");
    }
}

package com.avatar.publicfeed;

import android.util.Log;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.Map;

import hod.api.hodclient.HODClient;
import hod.api.hodclient.IHODClientCallback;

public class HODClientCallback implements IHODClientCallback {

    private HODClient hodClient;
    private static final String TAG = "HODClientCallback";

    public HODClientCallback(String apiKey) {
        hodClient = new HODClient(apiKey, this);
    }

    @Override
    public void requestCompletedWithContent(String response) {

    }

    @Override
    /*
    Asynchronous
     */
    public void requestCompletedWithJobID(String response) {
        try {
            JSONObject mainObject = new JSONObject(response);
            if (!mainObject.isNull("jobID")) {
                String jobID = mainObject.getString("jobID");
                hodClient.GetJobResult(jobID);
            }
        } catch (JSONException e) {
            Log.e(TAG, "Error in getting async response!!");
            e.printStackTrace();
        }
    }

    @Override
    public void onErrorOccurred(String errorMessage) {
        Log.e(TAG, errorMessage);
    }

    public void getRequest(Map<String, Object> params, String hodApp, hod.api.hodclient.HODClient.REQ_MODE mode) {
        Log.d(TAG, "sending request to server");

    }
}

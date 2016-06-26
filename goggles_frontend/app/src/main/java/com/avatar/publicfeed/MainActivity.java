package com.avatar.publicfeed;

import android.content.Intent;
import android.net.Uri;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.widget.AdapterView;
import android.widget.SearchView;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import hod.api.hodclient.HODApps;
import hod.api.hodclient.HODClient;
import hod.api.hodclient.IHODClientCallback;
import hod.response.parser.HODErrorCode;
import hod.response.parser.HODErrorObject;
import hod.response.parser.HODResponseParser;
import hod.response.parser.SpeechRecognitionResponse;

public class MainActivity extends AppCompatActivity implements IHODClientCallback {

    private static final boolean DEBUG = true;

    private static final String TAG = "PublicFeed:MainActivity";
    private static String API_KEY = "OUR_API_KEY";
//    private HODClientCallback hodClientCallback;
    private HODResponseParser hodResponseParser;
    private HODClient hodClient;

    private Button mButton;
    private ListView mListView;
    private CardView mCardView;

    private SearchView mSearchView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
//        startService(new Intent(this, ControllerService.class));
//        hodClientCallback = new HODClientCallback(API_KEY);
        hodClient = new HODClient(API_KEY, this);
        hodResponseParser = new HODResponseParser();

        mSearchView = (SearchView) findViewById(R.id.search_view_bar);
        mButton = (Button) findViewById(R.id.search_button);
        mListView = (ListView) findViewById(R.id.search_list_view);

        mButton.setOnClickListener(mSearchListener);
        mSearchView.setFocusable(true);
        mListView.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                ResponseData.Document document = (ResponseData.Document) mListView.getItemAtPosition(position);
                if (DEBUG) {
//                    Toast.makeText(getApplicationContext(), "position " + position + document.heading, Toast.LENGTH_SHORT).show();
                    Toast.makeText(getApplicationContext(), document.url, Toast.LENGTH_LONG).show();
                }
                String url = document.url;
                Intent intent = new Intent(Intent.ACTION_VIEW);
//                intent.setData(Uri.parse("http://google.com"));
                intent.setData(Uri.parse(url));
                view.getContext().startActivity(intent);
            }
        });
    }

//    public void enableLogoInActionBar() {
//        getSupportActionBar().setDisplayShowHomeEnabled(true);
//        getSupportActionBar().setLogo(R.drawable.app_logo);
//        getSupportActionBar().setDisplayUseLogoEnabled(true);
//        getSupportActionBar().setDisplayShowTitleEnabled(true);
//        getSupportActionBar().setDisplayShowHomeEnabled(true);
//        getSupportActionBar().setIcon(R.drawable.app_logo);
//    }


    @Override
    protected void onResume() {
        super.onResume();

    }

    private View.OnClickListener mSearchListener = new View.OnClickListener() {
        @Override
        public void onClick(View v) {
            if (mSearchView.getQuery().toString().equalsIgnoreCase("")) {
                return;
            }
            if (DEBUG) {
                Toast.makeText(getApplicationContext(), "making search " + mSearchView.getQuery(), Toast.LENGTH_SHORT).show();
            }
            makeQueryTextRequest();
//            simulateQueryTextRequest();
        }
    };

    private void highlightWord(String query) {

    }

    public String getQuery() {
        return mSearchView.getQuery().toString();
    }

    private void simulateQueryTextRequest() {
        String reference = "http://www.theatlantic.com/magazine/archive/2016/04/the-obama-doctrine/471525/";
        String heading = "Obama's Interview";
        String summary = "The U.S. President talks through his hardest decisions about America's role in the world.";
        String url = "http://www.theatlantic.com/magazine/archive/2016/04/the-obama-doctrine/471525/";
        String metadata = "city, san francisco";
        ResponseData responseData = new ResponseData();
        responseData.documents = new ArrayList<ResponseData.Document>();
        for (int i = 0; i < 10; i++) {
            responseData.documents.add(responseData.new Document(reference, summary, heading, url, metadata));
        }
        SearchAdapter adapter = new SearchAdapter(this, responseData.documents, mSearchView.getQuery().toString());
        mListView.setAdapter(adapter);

    }

    void makeQueryTextRequest() {
        String hodApp = HODApps.QUERY_TEXT_INDEX;
        Map<String,Object> params =  new HashMap<String,Object>();
        params.put("text", mSearchView.getQuery());
        params.put("indexes", "publicmeetings2");
//        params.put("indexes", "wiki_eng");
//        params.put("indexes", "world_factbook");
//        params.put("indexes", "news_eng");
        params.put("summary", "context");
        params.put("ignore_operators", "false");
        params.put("total_results", "false");
        params.put("print_fields", "heading, url, metadata");
        Log.d(TAG, "making POST query request " + params.toString());
        hodClient.PostRequest(params, hodApp, HODClient.REQ_MODE.SYNC);
    }

    @Override
    public void requestCompletedWithContent(String response) {
        //Synchronous
        if (DEBUG) {
            Toast.makeText(getApplicationContext(), "sync search successful", Toast.LENGTH_SHORT).show();
        }
        ResponseData responseData = (ResponseData) hodResponseParser.ParseCustomResponse(ResponseData.class, response);
        if (responseData != null && responseData.documents != null) {
            List<ResponseData.Document> documentList = responseData.documents;
            SearchAdapter adapter = new SearchAdapter(this, documentList, mSearchView.getQuery().toString());
            mListView.setAdapter(adapter);

//            for (ResponseData.Document document : responseData.documents) {
//                // TODO: access documents and populate
//                if (document != null) {
//                    if (DEBUG) {
//                        Toast.makeText(getApplicationContext(), document.heading, Toast.LENGTH_SHORT).show();
//                    }
//                } else {
//                    if (DEBUG) {
//                        Toast.makeText(getApplicationContext(), "sync search Doc null", Toast.LENGTH_SHORT).show();
//                    }
//                }
//            }
        } else {
            if (DEBUG) {
                Toast.makeText(getApplicationContext(), "sync search successful but null", Toast.LENGTH_SHORT).show();
            }
            List<HODErrorObject> errors = hodResponseParser.GetLastError();
            String errorMessage = "";
            for (HODErrorObject error : errors) {
                if (error.error == HODErrorCode.QUEUED) {
                    // sleep for few seconds and then check the job status again
                    hodClient.GetJobStatus(error.jobID);
                    return;
                } else if (error.error == HODErrorCode.IN_PROGRESS) {
                    hodClient.GetJobStatus(error.jobID);
                    return;
                } else {
                    errorMessage += String.format("Error code: %d\nError reason: %s\n", error.error, error.reason);
                    if (error.detail != null) {
                        errorMessage += "Error detail: " + error.detail + "\n";
                    }
                }
            }
            Log.e(TAG, errorMessage);
        }
        try {
            JSONObject mainObject = new JSONObject(response);
            if (!mainObject.isNull("jobID")) {
                String jobID = mainObject.getString("jobID");
                hodClient.GetJobResult(jobID);
            }
        } catch (Exception ex) { }
    }

    @Override
    public void requestCompletedWithJobID(String response) {
        // Asynchronous
        if (DEBUG) {
            Toast.makeText(getApplicationContext(), "async search successful", Toast.LENGTH_SHORT).show();
        }

    }

    @Override
    public void onErrorOccurred(String errorMessage) {
        Log.e(TAG, "error returned by search: " + errorMessage);
        if (DEBUG) {
            Toast.makeText(getApplicationContext(), "error returned by search", Toast.LENGTH_SHORT).show();
        }
    }
}

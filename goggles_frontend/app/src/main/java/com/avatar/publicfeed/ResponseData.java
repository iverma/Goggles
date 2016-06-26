package com.avatar.publicfeed;

import android.util.Log;

import java.util.List;


public class ResponseData {
    public List<Document> documents;

    public class Document {
        public String reference;
        public String summary;
        public String heading;
        public String url;
        public String metadata;

        public Document(String reference, String summary, String heading, String url, String metadata) {
            this.heading = heading;
            this.summary = summary;
            this.reference = reference;
            this.url = url;
            this.metadata = metadata;
        }
    }
}

package com.avatar.publicfeed;

import android.content.Context;
import android.graphics.Paint;
import android.support.v7.widget.CardView;
import android.text.Html;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.List;

public class SearchAdapter extends ArrayAdapter<ResponseData.Document> {

    String query;

    public SearchAdapter(Context context, int resource) {
        super(context, resource);
    }

    public SearchAdapter(Context context, List<ResponseData.Document> documents, String query) {
        super(context, 0, documents);
        this.query = query.toLowerCase();
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        ResponseData.Document document = getItem(position);
        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.item_search, parent, false);
        }

        TextView searchTitle = (TextView) convertView.findViewById(R.id.search_title);
        TextView searchSummary = (TextView) convertView.findViewById(R.id.search_summary);
        TextView searchMetadata = (TextView) convertView.findViewById(R.id.search_metadata);

        searchTitle.setText(document.heading);
        String summary = document.summary.toLowerCase();
        summary = summary.replaceAll(query, "<font color=#303F9F><b>" + query + "</b></font>");
        searchSummary.setText(Html.fromHtml(summary));
        searchMetadata.setText(document.metadata);
        searchTitle.setPaintFlags(searchTitle.getPaintFlags() |   Paint.UNDERLINE_TEXT_FLAG);
        return convertView;
    }
}

package com.aakankashas.template_adder;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.File;
import java.io.FileOutputStream;

public class MainActivity extends AppCompatActivity {

    private static final int PICK_PDF_FILE = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void selectAndUploadFile(View view) {
        Intent intent= new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.addCategory(Intent.CATEGORY_OPENABLE);
        intent.setType("application/pdf");

        startActivityForResult(intent, PICK_PDF_FILE);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent resultData) {
        super.onActivityResult(requestCode, resultCode, resultData);
        if (requestCode == PICK_PDF_FILE
                && resultCode == Activity.RESULT_OK) {
            Uri inPDF = null;
            String outPDF = "ABC";
            if (resultData != null) {
                inPDF = resultData.getData();
                Log.i("SelectAndUpload", "onActivityResult: " + inPDF);

                if (!Python.isStarted()) {
                    Python.start(new AndroidPlatform(MainActivity.this));
                }

                Python py = Python.getInstance();
                PyObject module = py.getModule("main");

                try {
                    PyObject result = module.callAttr("createPDFWithTemplate", inPDF, outPDF);
//                    PdfDocument resultPdf = new PdfDocument(result.toByte());
                    File dir = Environment.getExternalStorageDirectory();
                    File file = new File(dir, outPDF);
                    Log.i("Result PDF", String.valueOf(result.size()));
                    FileOutputStream op= new FileOutputStream(file);
                    op.write(result.toInt());
                } catch (Exception e) {
                    Log.i("Ex", "Exception!!!");
                    Toast.makeText(this, e.getMessage(), Toast.LENGTH_LONG).show();
                }

            }
        }
    }
}
package com.example.livestreamdemo.screens

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.camera.core.CameraSelector
import androidx.camera.core.Preview
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.Button
import androidx.compose.material.ButtonDefaults
import androidx.compose.material.Icon
import androidx.compose.material.Text
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLifecycleOwner
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import com.example.livestreamdemo.util.Common.REQUIRED_PERMISSIONS

@Composable
fun CameraPreviewScreen() {
    val lifecycleOwner = LocalLifecycleOwner.current
    val context = LocalContext.current
    val cameraProviderNext = remember { ProcessCameraProvider.getInstance(context) }


    var hasCamPermission by remember {
        mutableStateOf(
            REQUIRED_PERMISSIONS.all {
                ContextCompat.checkSelfPermission(context, it) ==
                        PackageManager.PERMISSION_GRANTED
            })
    }

    val launcher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions(),
        onResult = { granted ->
            hasCamPermission = granted.size == 2
        }
    )

    LaunchedEffect(key1 = true) {
        launcher.launch(
            arrayOf(
                Manifest.permission.CAMERA,
                Manifest.permission.WRITE_EXTERNAL_STORAGE
            )
        )
    }
    if (hasCamPermission) {
        AndroidView(
            factory = { ctx ->
                val previewView = PreviewView(ctx)
                val exec = ContextCompat.getMainExecutor(ctx)
                cameraProviderNext.addListener({

                    val cameraProvider = cameraProviderNext.get()
                    val preview = Preview.Builder().build()
                        .also {
                            it.setSurfaceProvider(previewView.surfaceProvider)
                        }

                    println(previewView.bitmap)
                    val cameraSelector = CameraSelector.Builder()
                        .requireLensFacing(CameraSelector.LENS_FACING_BACK)
                        .build()

                    cameraProvider.unbindAll()
                    cameraProvider.bindToLifecycle(
                        lifecycleOwner,
                        cameraSelector,
                        preview
                    )
                }, exec)
                previewView
            },
            modifier = Modifier.fillMaxSize(),
        )
    }
}

@Composable
fun RecordButton() {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(color = Color.Transparent)
            .offset(y = (600).dp)
    ) {
        Button(
            onClick = { /* record method */ },
            contentPadding = PaddingValues(
                start = 20.dp,
                top = 12.dp,
                end = 20.dp,
                bottom = 12.dp
            ),
            modifier = Modifier
                .align(Alignment.CenterHorizontally)
        ) {
            Spacer(Modifier.size(ButtonDefaults.IconSpacing))
            Text(text = "Record")
        }
    }
}
#include <stdio.h>
#include <stdlib.h>
#include <gst/gst.h>
#include <glib.h>

void confirmVersion();

int main(int argc, char *argv[]){

GMainLoop *loop;
GstElementFactory *factory;
GstElement *pipeline,*source,*filter,*encoder,*payloader,*sink;
GstCaps *caps;

gst_init (&argc, &argv);
loop = g_main_loop_new(NULL,FALSE);

confirmVersion();

pipeline = gst_pipeline_new("Aquabot_Cam_1");
source  = gst_element_factory_make("v4l2src","c270-source");
caps = gst_caps_new_simple("video/x-raw",
	"width",G_TYPE_INT,1280,
	"heght",G_TYPE_INT,720,NULL);
encoder = gst_element_factory_make("jpegenc","jpeg-encoder");
payloader = gst_element_factory_make("rtpjpegpay","jpeg-payloader");
sink = gst_element_factory_make("udpsink","network-sink");

if(!pipeline || !source || !caps || !encoder || !payloader || !sink){
	g_printerr("Failed to create one element. Exiting.\n");
	return -1;
}
g_object_set(G_OBJECT(source),"device","/dev/video0",NULL);
g_object_set(G_OBJECT(sink),"host","192.168.1.255",NULL);
g_object_set(G_OBJECT(sink),"port",7331,NULL);

//Add elements to pipeline
gst_bin_add_many(GST_BIN(pipeline),source,encoder,payloader,sink,NULL);

if(!gst_element_link_filtered(source,encoder,caps))
{
	printf("Failed to link caps!\n");
	return -1;
}
gst_caps_unref(caps);

//Link element pads
if (!gst_element_link_many (encoder,payloader, sink, NULL)) {
    g_warning ("Failed to link elements!");
}

gst_element_set_state(pipeline,GST_STATE_PLAYING);

printf("Playing");
g_main_loop_run(loop);

while(1){
}

gst_element_set_state(pipeline,GST_STATE_NULL);

gst_object_unref(pipeline);
g_main_loop_unref(loop);
//gst_object_unref(GST_OBJECT(source));
//gst_object_unref(GST_OBJECT(filter));
//gst_object_unref(GST_OBJECT(sink));

return 0;
}

void confirmVersion(){

const gchar *nano_str;
guint major, minor, micro, nano;

gst_version(&major,&minor,&micro,&nano);

if(nano == 1)
   nano_str = "(CVS)";
else if (nano == 2)
   nano_str = "(Prerelease)";
else
   nano_str = "";

printf("Built with GStreamer %d.%d.%d %s\n", major, minor, micro, nano_str);
}

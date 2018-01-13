#include <stdio.h>
#include <stdlib.h>
#include <gst/gst.h>
#include <glib.h>

int main(int argc, char *argv[]){

GMainLoop *loop;
GstElementFactory *factory;
GstElement *pipeline,*source,*filter,*sink,*element;
gchar *name;

const gchar *nano_str;
guint major, minor, micro, nano;

gst_init (&argc, &argv);
loop = g_main_loop_new(NULL,FALSE);

gst_version(&major,&minor,&micro,&nano);

if(nano == 1)
   nano_str = "(CVS)";
else if (nano == 2)
   nano_str = "(Prerelease)";
else
   nano_str = "";

printf("Built with GStreamer %d.%d.%d %s\n", major, minor, micro, nano_str);

pipeline = gst_pipeline_new("Aquabot_Cam_1");
source  = gst_element_factory_make("fakesrc","source");
filter = gst_element_factory_make("identity","filter");
//sink = gst_element_factory_make("updsink","sink");

 factory = gst_element_factory_find ("udpsink");
  if (!factory) {
    g_print ("Failed to find factory of type 'udpsink'\n");
    return -1;
  }
  sink = gst_element_factory_create (factory, "udpsink");
  if (!sink) {
    g_print ("Failed to create element, even though its factory exists!\n");
    return -1;
  }

g_object_set(G_OBJECT(sink),"host","192.168.1.255",NULL);
g_object_set(G_OBJECT(sink),"port",7331,NULL);

//Add elements to pipeline
gst_bin_add_many(GST_BIN(pipeline),source,filter,sink,NULL);

//Link element pads
if (!gst_element_link_many (source, filter, sink, NULL)) {
    g_warning ("Failed to link elements!");
}

gst_element_set_state(pipeline,GST_STATE_PLAYING);

g_main_loop_run(loop);

gst_element_set_state(pipeline,GST_STATE_NULL);

gst_object_unref(GST_OBJECT(pipeline));
g_main_loop_unref(loop);
//gst_object_unref(GST_OBJECT(source));
//gst_object_unref(GST_OBJECT(filter));
//gst_object_unref(GST_OBJECT(sink));

return 0;
}

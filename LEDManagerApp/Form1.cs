using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LEDManagerApp
{
    public partial class Form1 : Form
    {
        [DllImport("kernel32.dll")]
        public static extern Boolean AllocConsole();

        [DllImport("kernel32.dll")]
        public static extern Boolean FreeConsole();

        [DllImport("kernel32.dll")]
        public static extern Boolean AttachConsole(Int32 ProcessId);
        public Form1()
        {
            InitializeComponent();
            Hide();
            trayIcon.Visible = true;

            PerformanceCounter cpuCounter;
            PerformanceCounter ramCounter;
            cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total");
            ramCounter = new PerformanceCounter("Memory", "% Committed Bytes In Use");
            GPUMonitor gpuCounter = new GPUMonitor();

            //Color screenColor;
            Bitmap image;
            float cpuValue;
            float ramValue;
            float gpuValue;

            TcpClient client = new TcpClient();
            console.Text = console.Text + "Connecting.....\n";
            client.Connect(serverIp, serverPort);

            Stream stream = client.GetStream();

            int delay = 250;
            gpuCounter.InitGpuInfo();

            while (true)
            {

                cpuValue = cpuCounter.NextValue();
                ramValue = ramCounter.NextValue();
                gpuValue = gpuCounter.GetGpuInfo();

                console.Text = console.Text + $"{cpuValue}% {ramValue}% {gpuValue}%\n";
                console.Select(console.Text.Length - 1, 0);

                StatusPacket.SendPacket(stream, cpuValue, ramValue, gpuValue);

                Thread.Sleep(delay);
                Application.DoEvents();
            }
        }

        public const bool doImage = false;
        public const string serverIp = "129.11.102.134";
        public const int serverPort = 2610;

        private void Form1_Resize(object sender, EventArgs e)
        {
            //if the form is minimized  
            //hide it from the task bar  
            //and show the system tray icon (represented by the NotifyIcon control)  
            if (this.WindowState == FormWindowState.Minimized)
            {
                Hide();
                trayIcon.Visible = true;
            }
        }

        private void notifyIcon_MouseClick(object sender, MouseEventArgs e)
        {
            Show();
            this.WindowState = FormWindowState.Normal;
            trayIcon.Visible = false;
        }

    }

    public static class StatusPacket
    {
        struct Data
        {
            public float cpuUsage;
            public float ramUsage;
            public float gpuUsage;
        }

        public static void SendPacket(Stream stream, float cpuUsage, float ramUsage, float gpuUsage)
        {
            Data data = new Data();
            //data.image = image;
            data.cpuUsage = cpuUsage;
            data.ramUsage = ramUsage;
            data.gpuUsage = gpuUsage;


            int size = Marshal.SizeOf(data);
            byte[] dataBytes = new byte[size];

            IntPtr ptr = Marshal.AllocHGlobal(size);
            Marshal.StructureToPtr(data, ptr, true);
            Marshal.Copy(ptr, dataBytes, 0, size);
            Marshal.FreeHGlobal(ptr);

            SendBytes(stream, dataBytes);
        }

        public static void SendBytes(Stream stream, byte[] bytes)
        {
            if (stream.CanWrite)
            {
                stream.Write(bytes, 0, bytes.Length);
            }
            else
            {
                Console.WriteLine("Could not write data to stream as it has closed!");
            }
        }
    }
}

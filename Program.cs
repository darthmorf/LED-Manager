using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace LEDManager
{
    class Program
    {
        public const bool doImage = false;
        public const string serverIp = "129.11.102.134";
        public const int serverPort = 2610;
        public static void Main(string[] args)
        {
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
            Console.WriteLine("Connecting.....");
            client.Connect(serverIp, serverPort);

            Stream stream = client.GetStream();

            int delay = 250;
            gpuCounter.InitGpuInfo();

            while (true)
            { 

                cpuValue = cpuCounter.NextValue();
                ramValue = ramCounter.NextValue();
                gpuValue = gpuCounter.GetGpuInfo();

                Console.WriteLine($"{cpuValue}% {ramValue}% {gpuValue}%");

                if (doImage)
                {
                    image = new Bitmap(CaptureWindow(User32.GetDesktopWindow()));
                    StatusPacket.SendImagePacket(stream, image, cpuValue, ramValue, gpuValue);
                }
                else
                {
                    StatusPacket.SendPacket(stream, cpuValue, ramValue, gpuValue);
                }

                Thread.Sleep(delay);
            }
        }

        public static Image CaptureWindow(IntPtr handle)
        {
            // get te hDC of the target window
            IntPtr hdcSrc = User32.GetWindowDC(handle);
            // get the size
            User32.RECT windowRect = new User32.RECT();
            User32.GetWindowRect(handle, ref windowRect);
            int width = windowRect.right - windowRect.left;
            int height = windowRect.bottom - windowRect.top;
            // create a device context we can copy to
            IntPtr hdcDest = GDI32.CreateCompatibleDC(hdcSrc);
            // create a bitmap we can copy it to,
            // using GetDeviceCaps to get the width/height
            IntPtr hBitmap = GDI32.CreateCompatibleBitmap(hdcSrc, width, height);
            // select the bitmap object
            IntPtr hOld = GDI32.SelectObject(hdcDest, hBitmap);
            // bitblt over
            GDI32.BitBlt(hdcDest, 0, 0, width, height, hdcSrc, 0, 0, GDI32.SRCCOPY);
            // restore selection
            GDI32.SelectObject(hdcDest, hOld);
            // clean up 
            GDI32.DeleteDC(hdcDest);
            User32.ReleaseDC(handle, hdcSrc);
            // get a .NET image object for it
            Image img = Image.FromHbitmap(hBitmap);
            // free up the Bitmap object
            GDI32.DeleteObject(hBitmap);
            return img;
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

        public static void SendImagePacket(Stream stream, Bitmap image, float cpuUsage, float ramUsage, float gpuUsage)
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

            MemoryStream ms = new MemoryStream();
            image.Save(ms, ImageFormat.Jpeg);
            // read to end
            byte[] imageBytes = ms.GetBuffer();
            image.Dispose();
            ms.Close();

            SendBytes(stream, dataBytes);
            SendBytes(stream, imageBytes);
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

    public class GDI32
    {

        public const int SRCCOPY = 0x00CC0020; // BitBlt dwRop parameter
        [DllImport("gdi32.dll")]
        public static extern bool BitBlt(IntPtr hObject, int nXDest, int nYDest,
            int nWidth, int nHeight, IntPtr hObjectSource,
            int nXSrc, int nYSrc, int dwRop);
        [DllImport("gdi32.dll")]
        public static extern IntPtr CreateCompatibleBitmap(IntPtr hDC, int nWidth,
            int nHeight);
        [DllImport("gdi32.dll")]
        public static extern IntPtr CreateCompatibleDC(IntPtr hDC);
        [DllImport("gdi32.dll")]
        public static extern bool DeleteDC(IntPtr hDC);
        [DllImport("gdi32.dll")]
        public static extern bool DeleteObject(IntPtr hObject);
        [DllImport("gdi32.dll")]
        public static extern IntPtr SelectObject(IntPtr hDC, IntPtr hObject);
    }

    public class User32
    {
        [StructLayout(LayoutKind.Sequential)]
        public struct RECT
        {
            public int left;
            public int top;
            public int right;
            public int bottom;
        }
        [DllImport("user32.dll")]
        public static extern IntPtr GetDesktopWindow();
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindowDC(IntPtr hWnd);
        [DllImport("user32.dll")]
        public static extern IntPtr ReleaseDC(IntPtr hWnd, IntPtr hDC);
        [DllImport("user32.dll")]
        public static extern IntPtr GetWindowRect(IntPtr hWnd, ref RECT rect);
    }
}

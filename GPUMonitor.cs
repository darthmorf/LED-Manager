using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using OpenHardwareMonitor.Hardware;

namespace LEDManager
{
    class GPUMonitor
    {
        public class UpdateVisitor : IVisitor
        {
            public void VisitComputer(IComputer computer)
            {
                computer.Traverse(this);
            }
            public void VisitHardware(IHardware hardware)
            {
                hardware.Update();
                foreach (IHardware subHardware in hardware.SubHardware) subHardware.Accept(this);
            }
            public void VisitSensor(ISensor sensor) { }
            public void VisitParameter(IParameter parameter) { }
        }

        public List<int> i_ = new List<int>();
        public List<int> j_ = new List<int>();
        private bool initialised = false;
        public void InitGpuInfo()
        {
            initialised = true;
            UpdateVisitor updateVisitor = new UpdateVisitor();
            Computer computer = new Computer();
            computer.Open();
            computer.GPUEnabled = true;
            computer.Accept(updateVisitor);
            for (int i = 0; i < computer.Hardware.Length; i++)
            {
                if (computer.Hardware[i].HardwareType == HardwareType.GpuAti)
                {
                    i_.Add(i);
                    for (int j = 0; j < computer.Hardware[i].Sensors.Length; j++)
                    {

                        if (computer.Hardware[i].Sensors[j].SensorType == SensorType.Load)
                        {
                            j_.Add(j);
                        }
                    }

                    computer.Close();
                }
            }
            computer.Close();
        }
        public float GetGpuInfo()
        {
            if (!initialised)
            {
                return -1;
            }

            UpdateVisitor updateVisitor = new UpdateVisitor();
            Computer computer = new Computer();
            computer.Open();
            computer.GPUEnabled = true;
            computer.Accept(updateVisitor);
            foreach (int i in i_)
            {
                if (computer.Hardware[i].HardwareType == HardwareType.GpuAti)
                {
                    float? totalLoad = 0f;
                    foreach (int j in j_)
                    {
                        if (computer.Hardware[i].Sensors[j].SensorType == SensorType.Load)
                        {
                            totalLoad += computer.Hardware[i].Sensors[j].Value;
                        }
                    }

                    computer.Close();
                    return (float) totalLoad;
                }
            }
            computer.Close();
            return 0f;
        }
    }
}
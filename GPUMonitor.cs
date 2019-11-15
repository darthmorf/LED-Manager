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
        public string GetGpuInfo()
        {
            UpdateVisitor updateVisitor = new UpdateVisitor();
            Computer computer = new Computer();
            computer.Open();
            computer.GPUEnabled = true;
            computer.Accept(updateVisitor);
            for (int i = 0; i < computer.Hardware.Length; i++)
            {
                if (computer.Hardware[i].HardwareType == HardwareType.GpuAti)
                {
                    float? totalLoad = 0f;
                    for (int j = 0; j < computer.Hardware[i].Sensors.Length; j++)
                    {
                       
                        if (computer.Hardware[i].Sensors[j].SensorType == SensorType.Load)
                        {
                            totalLoad += computer.Hardware[i].Sensors[j].Value;
                        }
                    }

                    computer.Close();
                    return totalLoad.ToString();
                }
            }
            computer.Close();
            return "";
        }
    }
}
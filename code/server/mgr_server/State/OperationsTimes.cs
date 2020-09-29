using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace mgr_server.State
{
    public class OperationsTimes
    {
        public Func<int, int> OperationATimeFunc => a => a * 2;
        public Func<int, int> OperationBTimeFunc => a => a * 3;
        public Func<int, int> OperationCTimeFunc => a => a * 4;
        public Func<int, int> OperationDTimeFunc => a => a * 5;
    }
}

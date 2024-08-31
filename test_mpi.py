# test_mpi.py
from mpi4py import MPI
import unittest

class TestMPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.comm = MPI.COMM_WORLD
        cls.rank = cls.comm.Get_rank()
        cls.size = cls.comm.Get_size()

    @classmethod
    def tearDownClass(cls):
        MPI.Finalize()

    def test_size(self):
        """Test that the number of processes is as expected"""
        self.assertTrue(self.size > 0)
        self.assertEqual(self.size, MPI.COMM_WORLD.Get_size())

    def test_rank(self):
        """Test that ranks are assigned correctly"""
        self.assertTrue(0 <= self.rank < self.size)

    def test_send_recv(self):
        """Test simple send and receive operations"""
        if self.size < 2:
            self.skipTest("At least 2 MPI processes required")
        
        if self.rank == 0:
            data = {'key': 'value'}
            self.comm.send(data, dest=1)
        elif self.rank == 1:
            data = self.comm.recv(source=0)
            self.assertEqual(data, {'key': 'value'})

    def test_bcast(self):
        """Test broadcast operation"""
        if self.rank == 0:
            data = [1, 2, 3, 4, 5]
        else:
            data = None
        
        data = self.comm.bcast(data, root=0)
        self.assertEqual(data, [1, 2, 3, 4, 5])

    def test_scatter(self):
        """Test scatter operation"""
        if self.rank == 0:
            data = [i for i in range(self.size)]
        else:
            data = None
        
        local_data = self.comm.scatter(data, root=0)
        self.assertEqual(local_data, self.rank)

    def test_gather(self):
        """Test gather operation"""
        local_data = self.rank * 2
        gathered_data = self.comm.gather(local_data, root=0)
        
        if self.rank == 0:
            expected = [i * 2 for i in range(self.size)]
            self.assertEqual(gathered_data, expected)

if __name__ == '__main__':
    unittest.main()

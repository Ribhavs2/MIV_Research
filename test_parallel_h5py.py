# test_parallel_h5py.py
import unittest
import h5py
import os
import numpy as np
from mpi4py import MPI

class TestParallelH5PY(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.comm = MPI.COMM_WORLD
        cls.rank = cls.comm.Get_rank()
        cls.size = cls.comm.Get_size()
        cls.filename = 'test_parallel.h5'

    @classmethod
    def tearDownClass(cls):
        cls.comm.Barrier()
        if cls.rank == 0:
            if os.path.exists(cls.filename):
                os.remove(cls.filename)
        cls.comm.Barrier()  

    def test_parallel_write(self):
        """Test parallel writing to an HDF5 file"""
        with h5py.File(self.filename, 'w', driver='mpio', comm=self.comm) as f:
            dset = f.create_dataset('test', (self.size,), dtype='i')
            dset[self.rank] = self.rank

        self.comm.Barrier()

        with h5py.File(self.filename, 'r') as f:
            data = f['test'][:]
            self.assertEqual(data[self.rank], self.rank)
            self.assertEqual(len(data), self.size)

    def test_parallel_read(self):
        """Test parallel reading from an HDF5 file"""
        if self.rank == 0:
            with h5py.File(self.filename, 'w') as f:
                f.create_dataset('test', data=np.arange(self.size))

        self.comm.Barrier()

        with h5py.File(self.filename, 'r', driver='mpio', comm=self.comm) as f:
            data = f['test'][self.rank]
            self.assertEqual(data, self.rank)

    def test_collective_io(self):
        """Test collective I/O operations"""
        with h5py.File(self.filename, 'w', driver='mpio', comm=self.comm) as f:
            dset = f.create_dataset('test', (self.size,), dtype='i')
            with dset.collective:
                dset[self.rank] = self.rank * 2

        self.comm.Barrier()

        with h5py.File(self.filename, 'r', driver='mpio', comm=self.comm) as f:
            with f['test'].collective:
                data = f['test'][self.rank]
            self.assertEqual(data, self.rank * 2)

    def test_parallel_attribute(self):
        """Test setting and reading attributes in parallel"""
        # Write the file and set attribute
        if self.rank == 0:
            with h5py.File(self.filename, 'w') as f:
                dset = f.create_dataset('test', (self.size,), dtype='i')
                dset.attrs['description'] = 'Parallel test dataset'
        
        self.comm.Barrier()

        # Read the attribute in parallel
        with h5py.File(self.filename, 'r', driver='mpio', comm=self.comm) as f:
            attr = f['test'].attrs['description']
            self.assertEqual(attr, 'Parallel test dataset')


if __name__ == '__main__':
    unittest.main()

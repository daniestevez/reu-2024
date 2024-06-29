#!/usr/bin/env python3

import h5py
import numpy as np

import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', help='Output file path')
    parser.add_argument('--fft-bins', help='Number of FFT bins',
                        type=int, required=True)
    parser.add_argument('--bandwidth', help='Total bandwidth (Hz)',
                        type=float, required=True)
    parser.add_argument('--nint', help='Number of time integrations',
                        type=int, required=True)
    parser.add_argument('--freq', help='Center sky frequency (MHz)',
                        type=float, required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    x = np.fromfile(args.input_file, 'float32').reshape(-1, args.fft_bins)
    with h5py.File(args.output_file, 'w') as f_out:
        data = f_out.create_dataset('data', (x.shape[0], 1, args.fft_bins),
                                    dtype='f')
        data[:, 0] = x
        f_out.attrs['BITSHUFFLE'] = b'DISABLED'
        f_out.attrs['CLASS'] = b'FILTERBANK'
        f_out.attrs['VERSION'] = b'2.0'
        data.attrs['DIMENSION_LABELS'] = np.array(
            ['time', 'feed_id', 'frequency'], dtype='object')
        data.attrs['az_start'] = 0.0
        data.attrs['data_type'] = 1
        data.attrs['fch1'] = args.freq - 1e-6 * args.bandwidth / 2
        data.attrs['foff'] = 1e-6 * args.bandwidth / args.fft_bins
        data.attrs['ibeam'] = -1
        data.attrs['machine_id'] = 0
        data.attrs['nbeams'] = 1
        data.attrs['nbits'] = 32
        data.attrs['nchans'] = args.fft_bins
        # number of fine channels per coarse channel
        # here we only have one coarse channel
        data.attrs['nfpc'] = args.fft_bins
        data.attrs['nifs'] = 1
        data.attrs['rawdatafile'] = b''
        data.attrs['source_name'] = b''
        data.attrs['src_dej'] = 0.0
        data.attrs['src_raj'] = 0.0
        data.attrs['src_raj'] = 0.0
        data.attrs['telescope_id'] = 0
        data.attrs['tsamp'] = args.fft_bins * args.nint / args.bandwidth
        data.attrs['tstart'] = 60000.0  # MJD
        data.attrs['za_start'] = 0.0


if __name__ == '__main__':
    main()
